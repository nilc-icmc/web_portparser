import sys, os, datetime, random, base64, time
import streamlit as st
import streamlit.components.v1 as components
from tempfile import mkdtemp
from pathlib import Path
import pandas as pd

#-----Initial Parameters----

# Must be always False in production. When DEBUG is set to True the interface do not call the parser. Mode to debug interface features in local development.   
DEBUG=False
# Embedding model. Options are: 'bert-base-portuguese-cased' or 'bert-base-multilingual-uncased'
MODEL='bert-base-portuguese-cased'


#-----Fuctions-----

# Format external files for interface compatibility
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def img_to_html(img_path, img_style='max-width: 100%;'):
    img_html = f"<img src='data:image/png;base64,{img_to_bytes(img_path)}' style='{img_style}'>"
    return img_html

# Call parser steps
def make_conllu(path_text, path_input):
    try:
        os.system(f'python portTokenizer/portTok.py -o {path_input} -m -s S0000 {path_text}')
        return 'Converti o texto para conllu.'       
    except Exception as e:
        return str(e)
        
def make_embedding(path_input, path_embedding, model_selected):
    try:
        os.system(f'python ./wembedding_service/compute_wembeddings.py {path_input} {path_embedding} --model {model_selected}')
        return 'Fiz as embeddings.'
    except Exception as e:
        return str(e)


def make_predictions(path_input, path_prediction):
    try:
        os.system(f'python ./udpipe2/udpipe2.py Portparser_model --predict --predict_input {path_input} --predict_output {path_prediction}')
        return f'Fiz a predição.'
    except Exception as e:
        return str(e)

def make_sentences(path_raw_text, path_text):
    try:
        os.system(f'python portSentencer/portSent.py -o {path_text} -r -l 2048 {path_raw_text}')
        return f'Sentenciei.'
    except Exception as e:
        return str(e)


def get_predictions(path_prediction):
    try:
        with open(path_prediction, 'r') as f:
            st.text(f.read())
    except Exception as e:
        st.text('Resposta: '+e)


def run_pipeline(code,tmp_dir,path_text):
    
    input_conllu = 'input.conllu' 
    embedding_conllu = 'input.conllu.npz' 
    prediction_conllu = 'input_prediction.conllu'
    model = 'Portparser_model' 

    path_input = os.path.join(tmp_dir,f'{code}_{input_conllu}')
    path_prediction = os.path.join(tmp_dir,f'{code}_{prediction_conllu}')
    path_embedding = os.path.join(tmp_dir,f'{code}_{embedding_conllu}')

    with st.spinner('Transforming text into .conllu...'): 
        time.sleep(1)
        try:
            make_conllu(path_text, path_input)
        except Exception as e:
            print(e)
    with st.spinner('Processing embeddings...'): 
        time.sleep(1)
        try:
            make_embedding(path_input, path_embedding, model_selected)
        except Exception as e:
            print(e)
    with st.spinner('Making predictions...'): 
        time.sleep(1)
        try:
            make_predictions(path_input, path_prediction)
        except Exception as e:
            print(e)
    return path_prediction

#-----Debug mode-----

if DEBUG:
    tmp_dir = 'temp'
    code='0'
    input_text = 'text_input.txt'
else:
    tmp_dir = mkdtemp()
    code = f'{datetime.datetime.now().strftime("%d%m%Y_%H%M%S%f")+str(random.randint(0, 9))}'
    input_text = 'text_input.txt'

path_text = os.path.join(tmp_dir,f'{code}_{input_text}')
path_prediction = os.path.join('temp','0_input_prediction.conllu') # adicionei
area=0
with open(path_prediction, 'r', encoding='utf-8') as f:content = f.read().split('\n')


#-----Interface-----

with open('arborator-draft/arborator-draft.css','rb') as f: arborator_css = f.read().decode()
with open('style.css') as f: css = f.read()

st.set_page_config(page_title='Portparser', layout="wide")
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


# Grid
rowall = st.columns([2,26,2])

with rowall[1]:
    row2 = st.columns([6,4])

    # Head
    with row2[0]:
        st.markdown("<p id='logo-position'><b id='logo-title'><i>Portparser</i></b><br><b id='logo-subtitle'>A parsing model for Brazilian Portuguese</b></p>",unsafe_allow_html=True)
        st.markdown("<p class='text'> This is Portparser, a parsing model for Brazilian Portuguese that follows the <a href='https://universaldependencies.org/'>Universal Dependencies (UD)</a> framework.\
        We built our model by using a recently released manually annotated corpus, the Porttinari-base, \
        and we explored different parsing methods and parameters for training. We also test multiple embedding models and parsing methods. \
        Portparser is the result of the best combination achieved in our experiments.</p><p class='text'>Our model is explained in <a href='https://aclanthology.org/2024.propor-1.41/'>Lopes and Pardo (2024)</a>, and all datasets and full instructions to reproduce our experiments are\
        freely available at the <a href='https://github.com/LuceleneL/Portparser'>Portparser repository</a>. More details about this work may also be found at \
        the <a href='https://sites.google.com/icmc.usp.br/poetisa'>POeTiSA project webpage</a>.</p>",unsafe_allow_html=True)
        with st.expander('How to cite?', expanded=False):
            st.code("""
            @inproceedings{lopes2024towards,
                title={Towards Portparser-a highly accurate parsing system for Brazilian Portuguese following the Universal Dependencies framework},
                author={Lopes, Lucelene and Pardo, Thiago},
                booktitle={Proceedings of the 16th International Conference on Computational Processing of Portuguese},
                pages={401--410},
                year={2024}
            }""")
        
    with row2[1]:
        st.markdown(img_to_html('img/wordcloud_brasil5.png','width:100%; object-position: center top;'), unsafe_allow_html=True)

    # Mode to parse sentence 
    mode1, mode2 = st.tabs(['Single sentence', 'Multiple sentences'])
    
    # 'Single sentence'
    with mode1:
        rowmode1 = st.columns([1,28,1])

        with rowmode1[1]:
            st.write('Write a sentence and run to parse:')
            with st.form("parser"):
                text = st.text_input('Text: ')+' '
                print("TEXTO",text,"TEXTO")
                model_selected = MODEL+'-last4'
                submit = st.form_submit_button('Run')

            tab3, tab2, tab1 = st.tabs(["Tree","Table","Raw"])

            #with open(path_prediction, 'r', encoding='utf-8') as f: content = f.read()

            if submit:
                if not text.strip(): st.text("Can not parse empty text. Write a text above to parse.")                
                else:
                    try:
                        with open(path_text,'w',encoding='utf-8') as f: f.write(text)
                        if not DEBUG: path_prediction = run_pipeline(code,tmp_dir,path_text)
                        area=650
                        #else: path_prediction = os.path.join('temp','0_input_prediction.conllu')

                        with open(path_prediction, 'r', encoding='utf-8') as f:
                            content = f.read()

                            tab1.text(content)

                            input_conllu = 'input.conllu'
                            path_input = os.path.join(tmp_dir,f'{code}_{input_conllu}')
                            
                            content = content.split('\n')
                            table = pd.DataFrame([line.split('\t') for line in content[4:]])
                            table.columns = ['ID','FORM','LEMMA','UPOS','XPOS','FEATS','HEAD','DEPREL','DEPS','MISC']
                            tab2.dataframe(table[:-2], use_container_width=True,hide_index=True)

                    except Exception as e:
                            st.text('Não deu certo a predição.'+str(e)+repr(e))


            with tab3:
                # Prepare UD tree
                content_str = '\n'.join(content)
                components.html(
                '<style>'+open('arborator-draft/arborator-draft.css','rb').read().decode()+'</style>'+
                #'<style>{arborator_css}</style>'+
                """
                <script language="JavaScript" type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/d3/4.10.0/d3.js"></script>
                <script src="https://code.jquery.com/jquery-3.2.1.min.js" integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=" crossorigin="anonymous"></script>
                """+
                '<script>'+open('arborator-draft/arborator-draft.js','rb').read().decode()+'</script>'+
                f'<conll>{content_str}</conll>'+
                '<script>new ArboratorDraft();</script>',height=area)
               

    # 'Multiple sentences'
    with mode2:
        rowmode2 = st.columns([1,13,1,14,1])
        predictions = False
        with rowmode2[3]:
            explanation  = 'Upload a text file in order to parse multiple sentences. The file must be in a txt format with one sentence per line. \
                In case you have multiple sentences altogether, first select the option "Segment text for me" below, and we split it in lines for you.'
            option1, option2 = 'Text is ready (one sentence per line)','Segment text for me'
            split_option = st.radio(explanation,[option1,option2])

        with rowmode2[1]:
            with st.form("uploadfile_parser"):
                uploaded_file = st.file_uploader("Choose a file")
                submit = st.form_submit_button('Run')
           
            if submit:
                if uploaded_file is not None:
                    # Segment text first 
                    if split_option==option2:
                        path_raw_text = path_text[:-3]+'_raw.txt'
                        with open(path_raw_text, 'w') as f: f.write(uploaded_file.read().decode('utf-8'))
                        make_sentences(path_raw_text, path_text)
                    # Do not segment text first    
                    else:
                        with open(path_text,'w', encoding="utf-8") as f:f.write(uploaded_file.read().decode('utf-8')+' ')
                    if not DEBUG: path_prediction = run_pipeline(code,tmp_dir,path_text)
                    st.download_button( 
                        label="Download predictions",
                        data=open(path_prediction, 'r', encoding='utf-8').read(),
                        file_name='predictions.conllu'
                        )
                    predictions = True
                else:
                    st.text('Submit a text file to parse.')

        if predictions:
            row1mode2 = st.columns([1,28,1])
            with row1mode2[1]:
                tab1mode2, tab2mode2 = st.tabs(["Sentences","Result"])
                tab1mode2.text(open(path_text,"r").read())
                tab2mode2.text(open(path_prediction,"r").read())


                



    # Foot
    with st.container():
        logorow1 = st.columns([7,4,1,4,1,4,7])
        with logorow1[1]:      
            st.markdown("<a href='https://www.icmc.usp.br/'>"+img_to_html('img/icmc.png')+"</a>",unsafe_allow_html=True)
        with logorow1[3]:      
            st.markdown("<a href='https://c4ai.inova.usp.br/pt/inicio/'>"+img_to_html('img/c4ia.png')+"</a>",unsafe_allow_html=True)
        with logorow1[5]:
            st.markdown("<a href='https://sites.google.com/view/nilc-usp/'>"+img_to_html('img/nilc-removebg.png','max-width:80%')+"</a>",unsafe_allow_html=True)

        logorow2 = st.columns([7,4,1,4,1,5,7])
        with logorow2[1]:      
            st.markdown("<a href='https://inova.usp.br/'>"+img_to_html('img/inova_nobackground.png')+"</a>",unsafe_allow_html=True)
        with logorow2[3]:
            st.markdown("<a href='https://softex.br/'>" + img_to_html('img/softex_nobackground.png') + "</a>",unsafe_allow_html=True)
        with logorow2[5]:      
            st.markdown("<a href='https://www.gov.br/mcti/pt-br'>" + img_to_html('img/mcti_nobackground.png') + "</a>",unsafe_allow_html=True)

        logorow3 = st.columns([7,4,1,4,1,4,7])
        with logorow3[3]:      
            st.markdown("<a href='https://www.motorola.com.br/'>"+img_to_html('img/motorola_nobackground.png', 'max-width:70%; object-position: center bottom')+"</a>",unsafe_allow_html=True)

        creditrow = st.columns([7,14,7])
        with creditrow[1]:      
            st.markdown('<p style="text-align: center;margin-top:10px"> Designed and developed by Ana Carolina Rodrigues\
            <a href="https://github.com/anasampa"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-github" viewBox="0 0 16 16">\
            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8"/>\
            </svg></i></a><br>You may also contact the authors of the Portparser model.</p>',unsafe_allow_html=True)





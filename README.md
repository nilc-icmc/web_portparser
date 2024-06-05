# Portaparser Web Paser
We develop this project to provide an interactive online parser for Brazilian Portuguese that follows the Universal Dependencies (UD) framework running a specific model, the <a href='https://github.com/LuceleneL/Portparser'>Portaparser</a>.

You can access the web parser <a href='http://200.144.192.75:8082/'>here<a>.

Portaparser model was trained in the recently released manually annotated corpus, the Porttinari-base. This trained model is the result of the best combination achieved different our experiments that tested parsing methods, hiperparameters and embedding models. For more details about it see <a>Lopes and Pardo (2024)<a>.

The web parser make use of the parser code of <a href='https://github.com/ufal/udpipe'>UDPipe2</a> to run Portaparser (Portparser model was trained in it), the <a href='https://github.com/ufal/wembedding_service'>wembedding_service</a> to generate embeddings for the model, and <a href='https://github.com/Arborator/arborator-draft'>arborator</a> to provide the visualization of the dependency trees.  
In order to prevent possible pipeline breaks due to changes in the original codes, we incorporate and adapt part of the code from the original tools in this project. Please check the license from the original repositories of each one before making use of it.  




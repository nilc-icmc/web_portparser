# Web Parser Portparser
We developed this project to provide an interactive online parser for Brazilian Portuguese that follows the <a href='https://universaldependencies.org/'>Universal Dependencies (UD)</a> framework running a specific trained model, <a href='https://github.com/LuceleneL/Portparser'>Portaparser</a>. You can access the web parser <a href='http://200.144.192.75:8082/'>here<a>.</a>

This work is part of the POeTiSA project, a project from the Natural Language Processing initiative (NLP2) of the <a href='https://c4ai.inova.usp.br/'>Center for Artificial Intelligence (C4AI)</a> of the <a href='https://www5.usp.br/'>University of São Paulo</a>.

The web parser makes use of the parser code of <a href='https://github.com/ufal/udpipe'>UDPipe2</a> to run Portaparser (the Portparser model was trained in it), the <a href='https://github.com/ufal/wembedding_service'>wembedding_service</a> to generate embeddings for the model, and the <a href='https://github.com/Arborator/arborator-draft'>arborator</a> to provide the visualization of the dependency trees.  
In order to prevent potential pipeline breaks due to changes in the original codes, we incorporate and adapt part of the code from the original tools in this project. Please check the license from the original repositories of each one before making use of it.

The Portaparser model was trained in the recently released manually annotated corpus, the Porttinari-base. This trained model results from the best combination achieved in experiments that tested different parsing methods, hyperparameters, and embedding models. For more details about it see <a href='https://aclanthology.org/2024.propor-1.41/'>Lopes and Pardo (2024)</a>.

![image](https://github.com/anasampa/web_portparser/assets/36799215/ce6ddf2d-3905-477d-8e87-94ea5e81cccf)

![image](https://github.com/anasampa/web_portparser/assets/36799215/d0af3d07-c2fa-4d14-8f48-78124db6f516)






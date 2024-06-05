# Parser web
We develop this project to provide an interactive online parser for Brazilian Portuguese that follows the Universal Dependencies (UD) framework and run a specific model, the <a href='https://github.com/LuceleneL/Portparser'>Portaparser</a>.
The web app has a easy-to-use interface that runs uses <a href='https://github.com/ufal/udpipe'>UDPipe2</a> combine with Portaparser trained model

The web parser make use of the parser code of <a href='https://github.com/ufal/udpipe'>UDPipe2</a> to run Portaparser (Portparser model was trained in it), the <a>wembedding_service</a> to generate embeddings for the model, and <a href='https://github.com/Arborator/arborator-draft'>arborator</a> to provide the visualization of the dependency trees.  
In order to prevent possible pipeline breakes due to changes in the original code of the mentionate tools, the we incorporate the part of the code we use in this project. Please check the license from the original repositories of each one before making use of it.  

 
Portaparser model was trained in the recently released manually annotated corpus, the Porttinari-base. and we explored different parsing methods and parameters for training. We also test multiple embedding models and parsing methods. Portparser is the result of the best combination achieved in our experiments.

Our model is explained in Lopes and Pardo (2024), and all datasets and full instructions to reproduce our experiments are freely available at the Portparser repository. More details about this work may also be found at the POeTiSA project webpage.




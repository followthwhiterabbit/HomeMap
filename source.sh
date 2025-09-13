#!/bin/bash 
install_requirements(){

	pip3 install -r requirements.txt 

}

source_env(){
	source venv/bin/activate && echo "sourcing succeeded" || echo "sourcing failed"		
} 

generate_ui(){

	pyuic6 mainwindow.ui -o MainWindow.py && \
		echo "User interface file is generated successfully" || \
		echo "User interface file generation failed"

}

source_env
echo -ne '##### 			(33%)\r'
sleep 1
install_requirements 
echo -ne '############# 		(66%)\r'
sleep 1
generate_ui
echo -ne '############################  (100%)\r'
sleep 1

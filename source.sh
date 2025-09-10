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
install_requirements
generate_ui

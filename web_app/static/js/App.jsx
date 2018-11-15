import React from 'react';

//import styles
import '../css/App.css';
//import components
import DisplayManager from './displayManager.jsx';
export default class App extends React.Component {
	constructor(props,context){
		super(props,context);

		this.state = {
			currentDisplay: 'runDisplay'
		};
		this.goToNewCheck = this.goToNewCheck.bind(this);
		this.goToRunDisplay = this.goToRunDisplay.bind(this);
	}

	//Display
	render(){
		return(
			<div id="top">
				<div id="header">
					<button
						onMouseDown={this.goToRunDisplay}
					>View Data</button>
					<button
						onMouseDown={this.goToNewCheck}
					>New Check</button>
					
				</div>
				<div id="content">
					<DisplayManager className={this.state.currentDisplay}/>
				</div>
			</div>
		);
	}
	//State Management
	goToNewCheck(e){
		console.log('check');
		this.setState({currentDisplay: 'startCheckMenu'});
		e.stopPropagation();
	}
	goToRunDisplay(e){
		this.setState({currentDisplay: 'runDisplay'});
		e.stopPropagation();
	}

}

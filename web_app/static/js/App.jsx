import React from "react";
//import styles
import "../css/App.css";
//import components
import NewRunMenu from "./newRunMenu";
import NewRunButton from "./newRunButton";
import DataDisplay from "./dataDisplay";
export default class App extends React.Component {
	constructor(props,context){
		super(props,context);

		this.state = {
			menuVisible: false
		};
		this.getSampleData = this.getSampleData.bind(this);
		this.handleMenuClick = this.handleMenuClick.bind(this);
		this.toggleMenu = this.toggleMenu.bind(this);
	}

	//Display
	render(){
		return(
			<div id="top">
				<div id="header">
					<NewRunButton handleMouseDown={this.handleMenuClick}/>
				</div>
				<div>
					<NewRunMenu handleMouseDown={this.handleMenuClick} 
						menuVisibility={this.state.menuVisible}/>
				</div>
				<div id="content">
					<DataDisplay/>
				</div>
			</div>
		);
	}
	getSampleData(){
	
	}
	//State Management
	handleMenuClick(e){
		this.toggleMenu();

		console.log("menu toggled!")
		e.stopPropagation();
	}

	toggleMenu(){
		this.setState(
			{
				menuVisible: !this.state.menuVisible
			}
		);
	}


}

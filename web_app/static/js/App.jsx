import React from "react";
//import styles
import "../css/App.css";
//import components
import NewRunMenu from "./newRunMenu";
import NewRunButton from "./newRunButton";
export default class App extends React.Component {
	constructor(props,context){
		super(props,context);

		this.state = {
			menuVisible: false
		};

		this.handleMenuClick = this.handleMenuClick.bind(this);
		this.toggleMenu = this.toggleMenu.bind(this);
	}

	//Display
	render(){
		return(
			<div>
				<div id="header">
					<NewRunButton handleMouseDown={this.handleMenuClick}></NewRunButton>
				</div>
				<div id="dataDisplay">
					<NewRunMenu handleMouseDown={this.handleMenuClick} 
						menuVisibility={this.state.menuVisible}/>
					<ul>
						<li>physics</li>
						<li>is</li>
						<li>hard</li>
					</ul>
				</div>
			</div>
		);
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

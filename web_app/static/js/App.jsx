import React from "react";
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

	render(){
		return(
			<div>
				<p> this is just some meme'd placeholder content</p>
				<NewRunButton handleMouseDown={this.handleMenuClick}></NewRunButton>
				<NewRunMenu handleMouseDown={this.handleMenuClick} menuVisibility={this.state.menuVisible}/>
				<ul>
					<li>physics</li>
					<li>is</li>
					<li>hard</li>
				</ul>
			</div>
		);
	}
}

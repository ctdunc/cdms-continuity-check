import React, { Component } from 'react';
import RunDisplay from "./data-display/runDisplay.jsx";
import StartCheckMenu from "./continuity-ui/startCheckMenu.jsx";

export default class DisplayManager extends Component{
	constructor(props,context){
		super(props,context);
	}
	
	render(){
		switch(this.props.className){
			case "runDisplay":
				return(
				<div>
					<RunDisplay/>
				</div>
				);
				break;
			case "startCheckMenu":
				return(
					<div>
						<StartCheckMenu/>
					</div>
				);
				break;
			default:
				return(
				<div>
					<h1>invalid classname: {this.props.className}</h1>
				</div>
			);
		}
	}
}

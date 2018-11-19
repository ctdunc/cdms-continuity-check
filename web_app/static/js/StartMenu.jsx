import React, { Component } from 'react';
import StartMenuForm from './StartMenu_Form';
import StartMenuStatus from './StartMenu_Status';

class StartMenu extends Component{
	constructor(props,context){
		super(props,context);
	}
	render(){
		return(
			<div>
				<div className="left-50">
					<StartMenuForm className="left-50"/>
				</div>
				<div className="right-50">
					<StartMenuStatus className="right-50"/>
				</div>
			</div>
		);
	}
}
export default StartMenu;

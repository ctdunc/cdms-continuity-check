import React, { Component } from "react";
import '../css/NewRunMenu.css';
class NewRunMenu extends Component {
	render() {
		var visibility = "hide"

		if(this.props.menuVisibility){
			visibility = "show";
		}

		return (
			<div id="flyoutMenu" className={visibility} onMouseDown={this.props.handleMouseDown}>
				This is where there will be some menu component
			</div>
		);
	}
}

export default NewRunMenu;

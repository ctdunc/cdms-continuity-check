import React, { Component } from "react";
import '../../css/NewRunMenu.css';
class NewRunMenu extends Component {
	render() {
		var visibility = "hide"

		if(this.props.menuVisibility){
			visibility = "show";
		}

		return (
			<div id="flyoutMenu" className={visibility}> 
				<h1>Continuity Check</h1>

				<div id="exitMenu">
					<button className="start" onMouseDown={this.props.startTest}>Start Test</button>
					<button className="cancel" onMouseDown={this.props.handleMouseDown}>Cancel</button>
				</div>
			</div>
		);
	}
}

export default NewRunMenu;

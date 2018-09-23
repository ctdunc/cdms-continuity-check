import React, { Component } from "react";

class NewRunButton extends Component  {
	render() {
		return(
			<button id="newRunButton"
				onMouseDown={this.props.handleMouseDown}>New Check</button>
		);
	}
}

export default NewRunButton;


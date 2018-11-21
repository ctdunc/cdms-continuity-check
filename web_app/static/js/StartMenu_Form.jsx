import React, { Component } from 'react';
import Form from 'informed';

export default class StartMenu_Form extends Component{
	constructor(props,context){
		super(props,context);
	}

	render(){
		return(
			<div>
				<Form onChange={this.handleChange} id="startcheck-form">
					<label htmlFor="startcheck-validation">
					Expected Values:
					</label>
					<Select field="validtion" 
						id="select-validation"
						multiple
					>
				//TODO: add in logic to get from SQL table		{this.selectValues}
					</Select>
					
				</Form>
				<button onMouseDown={this.props.startTask} />
			</div>
		);
	}
}

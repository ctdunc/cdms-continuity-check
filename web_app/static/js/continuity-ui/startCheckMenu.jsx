import React, { Component } from 'react';
import Select from 'react-select';
import io from 'socket.io-client';
var $ = require('jquery');

import CheckLog from './checkLog';
export default class StartCheckMenu extends Component{
	constructor(props,context){
		super(props,context);
		this.state={};
	}
	
	
	render(){
		return(
			<div>
				<form onSubmit={this.handleFormSubmit} className="checkOpts">
					<div className="row">
						<label className="col-25">
							Expected Values
							<select name="expected_table" 
								value={this.props.expected_table} 
								onChange={this.handleInputChange} 
								className="col-75">	
								<option value='slac_expected_values'>slac</option>
								<option value='slac_2'>slac2</option>
							</select>
						</label>
					</div>
					<div className="row">
						<label className="col-25">
							Tests
							<Select
								value={this.state.tests}
								menuPortalTarget="tests"
								onChange={this.handleMultipleInputChange}
								isMulti={true}
								options={[{value: 'test1', label: 'test1'},{value:'test2',label:'test2'}]}
								className="col-75"
							/>
						</label>
					</div>
					<div className="row">
						<label className="col-25">
							Channels
						</label>
					</div>
					<div className="row">
						<label className="col-25">
							Institution
						</label>
					</div>
					<div className="row">	
						<label className="col-25">
							Wiring
						</label>
					</div>
					<div className="row">
						<label className="col-25">
							Device
						</label>
					</div>
					<div className="row">
						<label className="col-25">
							VIB
						</label>
					</div>
					<input type="submit" value="Submit"/>
				</form>	
			</div>
		);
	}
	handleInputChange(e){
		const target = e.target;
		console.log(target);
		const value = target.type === 'checkbox' ? target.checked : target.value;
		const name = target.name;
		this.setState({
			[name]: value
		});
}
}

import React, { Component } from 'react';
import Select from 'react-select';

export default class StartMenu_Form extends Component{
	constructor(props,context){
		super(props,context);
	}

	render(){
		return(
			<div>
			<form>
				<div className="row">
					<label className="col-25">
							Expected Values
						<select name="expected_table"
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
			<button onMouseDown={this.props.startTask} />
			</div>
		);
	}
}

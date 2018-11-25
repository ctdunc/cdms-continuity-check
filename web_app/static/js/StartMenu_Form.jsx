import React, { Component } from 'react';
import { Form, Select, Option } from 'informed';

export default class StartMenu_Form extends Component{
	constructor(props,context){
		super(props,context);
		this.state = {
			'expected-values': '',
			'tests': [],
			'institution': '',
			'wiring': '',
			'vib': '',
			'device': ''
		}
		this.setFormApi = this.setFormApi.bind(this);
		this.handleChange = this.handleChange.bind(this);
	}
	
	setFormApi(formApi){
		this.formApi = formApi;
	}
	handleChange(){
		
	}
	render(){
		return(
			//FORM NEEDS: validation, tests, temperature, institution, wiring, VIB, device 
			<div>
				<Form getApi={this.setFormApi} id="startcheck-form">
					<div className="row">
						<label className="col-25">
							Expected Values:
						</label>
						<Select field="expected-values" className="col-75">
							<Option value="" disabled>
								Select One...
							</Option>
						</Select>
					</div>
					<div className="row">
						<label className="col-25">
							Tests:	
						</label>
						<TestSelector/> 
					</div>
					<div className="row">
						<label className="col-25">
							Institution:
						</label>
						<Select field="institution" className="col-75">
							<Option value="" disabled>
								Select One...
							</Option>
						</Select>
					</div>
					<div className="row">
						<label className="col-25">
							Wiring:
						</label>
						<Select field="wiring" className="col-75">
							<Option value="" disabled>
								Select One...
							</Option>
						</Select>
					</div>
					<div className="row">
						<label className="col-25">
							VIB:
						</label>
						<Select field="vib" className="col-75">
							<Option value="" disabled>
								Select One...
							</Option>
						</Select>
					</div>
					<div className="row">
						<label className="col-25">
							Device:
						</label>
						<Select field="device" className="col-75">
							<Option value="" disabled>
								Select One...
							</Option>
						</Select>
					</div>
					<button type="submit">submit</button>
				</Form>
			</div>
		);
	}
}

class TestSelector extends Component {
	constructor(props,context){
		super(props,context);
	}

	render(){
		return(
			<div className="col-75">
				<div className="col-25">
					<label>
						Signal 1:
					</label>
					<br/>
					<Select field="signal-1"> 
						<Option value="" disabled>
							Select One...
						</Option>
					</Select>
				</div>
				<div className="col-75">
					<label>
						Signal 2:
					</label>
					<br/>
					<Select field="signal-2" multiple>
						<Option value="" disabled>
							Select Multiple
						</Option>
					</Select>
				</div>
			</div>
		);
	}
}

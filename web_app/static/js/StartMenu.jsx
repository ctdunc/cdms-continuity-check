import React, { Component } from 'react';
import StartMenuForm from './StartMenu_Form';
import StartMenuStatus from './StartMenu_Status';

var $ = require('jquery');

class StartMenu extends Component{
	constructor(props,context){
		super(props,context);
		this.state = {
			checkProps: {
				expected_table: '',
				tests: [],
				channels: [],
				institution: '',
				wiring: '',
				device: '',
				vib: ''
			},
			status_url: '',
			total: 0,
			complete: 0,
			running: false
		};

		this.startTask = this.startTask.bind(this);

	}
	startTask(e){
		$.ajax({
			type: 'POST',
			url: '/continuitycheck',
			success: ((data, stat, request)=> {
				this.setState({
					status_url: request.getResponseHeader('Location'),
					running: true
				});
			})
		});
		e.stopPropagation()
	}

	
	render(){
		return(
			<div>
				<div className="left-50">
					<StartMenuForm className="left-50"
						startTask={this.startTask}/>
				</div>
				<div className="right-50">
					<StartMenuStatus className="right-50"
						status_url={this.state.status_url}
					/>
				</div>
			</div>
		);
	}
}
export default StartMenu;

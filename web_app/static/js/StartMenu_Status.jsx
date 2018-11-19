import React, { Component } from 'react';

var $ = require('jquery');

export default class StartMenuStatus extends Component {
	constructor(props,context){
		super(props,context);
		this.state = {
			taskid: '',
			total: 0,
			complete: 0,
			messages: {},
			passes: {},
			fails: {}
		};

		this.startTask = this.startTask.bind(this);
		this.updateStatus = this.updateStatus.bind(this);
	}

	startTask(e){
		$.ajax({
			type: 'POST',
			url: '/taskstatus',
			success: ((data, stat, request)=> {
				var status_url = request.getResponseHeader('Location');
				this.updateStatus(status_url);
			})
		});
		e.stopPropagation();
	}
	
	updateStatus(status_url){
		$.getJSON(status_url, ((data)=> {
			if(data['state'] != 'PENDING' && data['state'] == 'PROGRESS') {
				if('result' in data){
					this.setState({messages: [...this.state.messages, data]});
					this.updateStatus(status_url);
				}
				else{
					this.setState({messages: [...this.state.messages, data]});
					this.updateStatus(status_url);
				}
			}
			else {
				setTimeout(() => {
					this.updateStatus(status_url);
				}, 2000);
			}
		}
		));
	}

	render(){
		return(
			<div>	
				<div className="status">
					// progress bar
					// message output
				</div>
				<div className="failureDisplay">
					
				</div>
				<div className="successDisplay">
				</div>
			</div>
		);
	}
}

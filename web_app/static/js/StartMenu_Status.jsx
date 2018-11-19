import React, { Component } from 'react';

var $ = require('jquery');

export default class StartMenuStatus extends Component {
	constructor(props,context){
		super(props,context);
		this.state = {
			status_url: this.props.status_url,
			messages: {},
			passes: {},
			fails: {},
			stat: 'Pending...'
		};

		this.updateStatus = this.updateStatus.bind(this);
		this.updateStatus();
	}

			
	updateStatus(status_url){
		if(status_url!=''){
		$.getJSON(status_url, ((data) => {
			if(data['state'] != 'PENDING' && data['state'] != 'PROGRESS'){
				this.setState({messages: [...this.state.messages, data['status']]});
			}
			else{
				if(data['state'] == 'PROGRESS'){
					value = data['value']
					if(data['key'] == 'MSG'){
						this.setState({messages: [...this.state.messages, value]});
					}
					else if (data['key']== 'MEASUREMENT'){
						if(value['passing']){
							this.setState({passes: [...this.state.passes, value]});
						}
						else{
							this.setState({fails: [...this.state.fails, value]});
						}
					}

					setTimeout(() => {
						this.updateStatus(status_url);
					}, 1000);
				}
					else {
						this.setState({messages: 'Unknown Worker State or Failure'});
					}
				}
		}));
	}}

	render(){
		return(
			<div>	
				<div className="status">
					{JSON.stringify(this.state)}
				</div>
				<div className="failureDisplay">
					fail
				</div>
				<div className="successDisplay">
					succ
				</div>
			</div>
		);
	}
}

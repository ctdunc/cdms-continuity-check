import React, { Component } from 'react';
import io from 'socket.io-client';
import StartMenuForm from './StartMenu_Form';
import StartMenuStatus from './StartMenu_Status';
var $ = require('jquery');
var socket = io.connect('http://' + document.domain + ':' + location.port);
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
			total: 0,
			complete: 0,
			running: false,
			messages: {},
			fails: {},
			passes: {}
		};

		this.startTask = this.startTask.bind(this);
		this.updateStatus = this.updateStatus.bind(this);
		this.emitEvent = this.emitEvent.bind(this);
		socket.on('connection',(socket) => {
			console.log('connection!');
			socket.emit('hello');
		});
	}
	emitEvent(e){
		socket.emit('hello');
		console.log('emitted');
		e.stopPropagation();
	}
	startTask(e){
		$.ajax({
			type: 'POST',
			url: '/continuitycheck',
			success: ((data, stat, request)=> {
				var status_url = request.getResponseHeader('Location');

				setTimeout(()=>{this.updateStatus(status_url)},200);
				})
			});
		e.stopPropagation()
	}

	updateStatus(status_url){
		$.getJSON(status_url, ((data) => {
			console.log(data);
			if(data['state'] != 'PENDING' && data['state'] != 'PROGRESS'){
				this.setState({messages: [...this.state.messages, data['status']]});
			}
			if(data['state'] == 'PENDING'){
				this.setState({messages: data['state']});
			}
			else{
				var value = data['value'];
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
				this.updateStatus(status_url);
			}
				}));
		}

		
	render(){
		return(
			<div>
				<button onMouseDown={this.emitEvent}> Emit Test</button>
				<div className="left-50">
					<StartMenuForm className="left-50"
						startTask={this.startTask}/>
					<div>
						{JSON.stringify(this.state.status_url)}
					</div>
				</div>
				<div className="right-50">
					{JSON.stringify(this.state.passes)}
					{JSON.stringify(this.state.fails)}
					{JSON.stringify(this.state.messages)}
				</div>
			</div>
		);
	}
}
export default StartMenu;

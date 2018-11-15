import React, { Component } from 'react';
import io from 'socket.io-client';
let socket = io('http://127.0.0.1:5000')

class CheckLog extends Component {
	constructor(props,context){
		super(props,context);
		this.state={data:'none yet'};
	}
	componentDidMount(){
	socket.on('connect', data => {
		socket.send('connection!');
	})
	}
}

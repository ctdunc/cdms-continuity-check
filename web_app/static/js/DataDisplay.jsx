import React, { Component } from 'react';
import ReactTable from 'react-table';
import 'react-table/react-table.css';

var $ = require('jquery');

const histCols = [
	{Header:"Date",accessor:'0'},
	{Header:"Institution",accessor:'1'},
	{Header:"VIB",accessor:'2'},
	{Header:"Wiring",accessor:'3'},
	{Header:"Device",accessor:'4'},
	{Header:"Temperature",accessor:'5'},
	{Header:"Validator",accessor:'6'}
]
const checkCols = [
	{Header: "Signal",
		columns: [
			{Header:"Signal 1",accessor:'0'},
			{Header:"Signal 2",accessor:'1'},
			]
	},
	{Header: "Continuity",
		columns: [
			{Header:"Minimum",accessor:'2'},
			{Header:"Maximum",accessor:'3'},
			{Header:"Measured",accessor:'4'},
			{Header:"Unit",accessor:'5'},
			{Header:"Passed",accessor:'6'}
		]}
]
class DataDisplay extends Component{
	constructor(props,context){
		super(props,context);
		this.state = {
			tableName: '', 
			data:[],
			columns: histCols
		};
		
		this.getRuns=this.getRuns.bind(this);
		this.displayRuns=this.displayRuns.bind(this);
		this.getCheck=this.getCheck.bind(this);
		this.displayCheck=this.displayCheck.bind(this);

		this.getRuns();
	}

	getCheck(tname){
		$.get(window.location.href+'continuity-history/'+tname,
			(data) =>{
				this.displayCheck(data,tname);
			}
		);
	}

	displayCheck(data,tname){
		this.setState({
			tableName: tname,
			data: data,
			columns: checkCols
		});
	}

	getRuns(){
		$.get(window.location.href+'continuity-history', 
			(data) =>{
				this.displayRuns(data);
			}
		);
	}

	displayRuns(data){
		this.setState({
			tableName: 'continuity_history',
			data: data,
			columns: histCols
		});
	}

	render(){
		return(
			<div>
				<ReactTable data={this.state.data}
					columns={this.state.columns}
					className="-striped -highlight"
				/>
			</div>
		);
	}
}
export default DataDisplay;

import React, { Component } from "react";
import ReactTable from "react-table";
var $ = require('jquery');
import "react-table/react-table.css";
import "../css/App.css"
class DataDisplay extends Component{
	constructor(props,context){
		super(props,context);
		this.getData=this.getData.bind(this)
		this.state={data:[],style:{}}
		this.tableName = props.tableName
		console.log(props.tableName);
		this.getData();
	}
	render(){
		return(
			<div>
				<ReactTable data={this.state.data} 
					columns={[
					{
						Header: "Signal",
						columns: [
							{
								Header: "Signal 1",
								accessor: '0'
							},
							{
								Header: "Signal 2",
								accessor: '1',
							}
						]},
						{
						Header: "Continuity",
						columns: [
						
						{
							Header: "Min",
							accessor: '2'
						},
						{
							Header:	"Max",
							accessor: '3'
						},
						{
							Header: "Measured",
							accessor:'4'
						},
						{
							Header:"unit",
							accessor:'5'
						},
						{
							Header:"Pass",
							accessor:'6'
						}
						]}
					]}
					className="-striped -highlight"
					style={this.state.style}
				/>
			</div>
		);
	}
	getData(){
		//tableName is the prop I want to work with
		$.get(window.location.href+'run/'+this.tableName, (data) => {
			this.updateData(data);
		}
		);
	}
	updateData(data){
		this.setState({data: data});
	}
}

export default DataDisplay;

import React, { Component } from "react";
import ReactTable from "react-table";
var $ = require('jquery');
import "react-table/react-table.css";
class DataDisplay extends Component{
	constructor(props,context){
		super(props,context);
		this.getData=this.getData.bind(this)
		this.state={data:[]}
		this.tableName = props.tableName
		console.log(props.tableName);
		this.getData();
	}
	render(){
		return(
			<div>
				<ReactTable data={this.state.data} 
					getTheadProps={() => {
							return {
								style: {
									background: "red",
								}
							}}}	
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
				/>
			</div>
		);
	}
	getData(){
		//tableName is the prop I want to work with
		$.get(window.location.href+'run/'+this.tableName, (data) => {
			this.updateData(data);
			console.log(this.props);
			console.log(data)
		}
		);
	}
	updateData(data){
		this.setState({data: data});
	}
}

export default DataDisplay;

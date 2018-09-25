import React, { Component } from "react";
import ReactTable from "react-table";
var $ = require('jquery');
import "react-table/react-table.css";
class DataDisplay extends Component{
	constructor(props,context){
		super(props,context);
		this.getData=this.getData.bind(this)
		this.state={data:[]}
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
							Header: "Expected Continuity",
							accessor: '2'
						},
						{
							Header: "Min",
							accessor: '3'
						},
						{
							Header:	"Max",
							accessor: '4'
						}
						]}
					]}
				/>
			</div>
		);
	}
	getData(){
		$.get(window.location.href+'expectedData', (data) => {
			this.updateData(data);
			console.log(data)
		}
		);
	}
	updateData(data){
		this.setState({data: data});
	}
}

export default DataDisplay;

import React, { Component } from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";
class DataDisplay extends Component{
	constructor(props,context){
		super(props,context);
		this.state = {
			data: {$.get(window.location.href+'expected_result')}
		};
		this.getData = this.getData.bind(this)
	}
	render(){
		return(
			<ReactTable
				data={this.state.data}
				columns={[
					{
						Header: "Test"
					},
					{
						Header: "Test 2"
					}]
				}
			/>
		);
	}
	getData(){
		$.get(window.location.href+'expected_result', (data) => {
			this.updateData(data);
		}
		);
	}
	updateData(data){
		this.setState({data: data});
	}
}

export default DataDisplay;

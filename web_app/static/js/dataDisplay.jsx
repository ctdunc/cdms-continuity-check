import React, { Component } from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";
class DataDisplay extends Component{
	constructor(props,context){
		super(props,context);

	}
	render(){
		return(
			<ReactTable
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
}

export default DataDisplay;

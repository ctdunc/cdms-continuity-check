import React, { Component } from "react";
import ReactTable from "react-table";
import DataDisplay from './dataDisplay';
var $ = require('jquery');
import "react-table/react-table.css";

class RunDisplay extends Component{
	constructor(props,context){
		super(props,context);
		this.getData=this.getData.bind(this)
		this.state={data:[]}
		this.getData();
	}
	render(){
		return(
			<div>
				<ReactTable 
					data={this.state.data}
					columns = {[
						{
							Header:"Date",
							accessor: '0',
							//render: {props => <span>{moment.utc(props.value).format('DD/MM/YYYY')}}</span>
						},
						{
							Header:"Institution",
							accessor: '1'
						},
						{
							Header:"VIB",
							accessor: '2'
						},
						{
							Header:"Wiring",
							accessor:'3'
						},
						{
							Header:"Device",
							accessor:'4'
						},
						{
							Header:"Temperature",
							accessor:'5'
						},
						{
							Header:"Validator",
							accessor:'6'
						}
				]}
					style={{
						height:"95vh",
						width:"100vw"
					}}
					className="-striped -highlight"
					SubComponent={row =>{
						return(
							<DataDisplay
								tableName={row.original[7]}
							/>

						);
					}}
					/>
			</div>
		);
	}
	getData(){
		$.get(window.location.href+'runHistory',(data)=>{
			this.updateData(data);
		}
		);
	}
	updateData(data){
		this.setState({data:data})
	}
}

export default RunDisplay;

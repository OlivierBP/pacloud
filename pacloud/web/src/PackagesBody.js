import React, { Component } from 'react';
import 'react-bootstrap';
import './Packages.css';
import data from './metadata.json';

class PackagesBody extends Component{
	constructor(props) {
		super(props);
		var tableau = [];
		this.creatBody(data, tableau);
		this.state={bdyRows:tableau};
	}

	componentWillReceiveProps(nextProps){
		var tableau = [];
		this.creatBody(nextProps.bdy, tableau);
		this.setState({bdyRows:tableau});	
	}

	creatBody (data, bdy_decl) {
		data.forEach(function(obj){
			var values = [];
			values.push({info:obj.value});
			bdy_decl.push({tab:values});
		});
	}

	render() {
                return(
                        <tbody>
                                {this.state.bdyRows.map(function (bdyRow, index)       
                                {      
                                        return <tr key={index}>{bdyRow.tab.map(function (bdyCell, index2){return(<td className={bdyCell.shade} key={index2.toString()}>{bdyCell.info}</td>);})}</tr>;
                                })}                           
                        </tbody>
                );
        }

};
export default PackagesBody;

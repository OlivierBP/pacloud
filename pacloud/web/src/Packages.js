import React, { Component } from 'react';
import {Table, Button} from 'react-bootstrap';
import data from './metadata.json';
import 'react-bootstrap';
import './Packages.css';
//import PackagesBody from './PackagesBody.js'

class Packages extends Component {

	/*constructor(props){
		super(props);
		this.state={base:'./metadata.json'}
	}*/


	render() {
		return(
			<div>		
				<Button bsStyle="danger" id="Update"> Update All</Button>		
				<Table id="table" bordered condensed hover>
					<thead>
						<tr>Packages</tr>
						<tr>
							<td>Name</td>
							<td>Description</td>
							<td>Versions</td>
						</tr>
					</thead>
					
					<tbody>
						<tr>
							<td>media-gfx/feh</td>
							<td>Fast and light imlib2-based image viewer</td>
							<td>
								<ul>
									<li>number: 2.23.2, dependencies: imlib2 <Button bsSize="small" bsStyle="primary" className="button">Remove</Button></li>
						 			<li>number: 2.25, dependencies: imlib2 <Button bsSize="small" bsStyle="danger" className="button">Install</Button></li>
								</ul>
							</td>
						</tr>
						<tr>
							<td>imlib2</td>
							<td>Image file loading library (required by: feh, ncurses)</td>
							<td>
								<ul>
									<li>number: 1.4.10 <Button bsSize="small" bsStyle="primary" className="button">Remove</Button></li>
								</ul>
							</td>
						</tr>
						<tr>
							<td>ncurses</td>
							<td>System V Release 4.0 curses emulation library</td>
							<td>
								<ul>
									<li>number: 6.1-r1, dependencies: imlib2 <Button bsSize="small" bsStyle="primary" className="button">Remove</Button></li>
								</ul>
							</td>
						</tr>
					</tbody>
				</Table>
			</div>
		);	
	}

};
export default Packages;


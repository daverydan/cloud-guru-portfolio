import React from "react";
import { shallow } from 'enzyme';
import ExampleWork, { ExampleWorkProject } from '../js/example-work';

const myWork = [
	// JS object literal
	{
		'title': "Work Example",
		'image': {
			'desc': "example screenshot of a project involving code",
			'src': "images/example1.png",
			'comment': ""
		}
	},
	{
		'title': "Work Example 2",
		'image': {
			'desc': "example screenshot of a project involving chemistry",
			'src': "images/example2.png",
			'comment': `“Chemistry” by Surian Soosay is licensed under CC BY 2.0
		               https://www.flickr.com/photos/ssoosay/4097410999`
		}
	}
];

describe("ExampleWork component", () => {
	let component = shallow(<ExampleWork work={myWork} />)

	it("Should be a 'section' element", () => {
		// does not return the components inside component being tested
		// console.log(component.debug()); // see what's returned
		expect(component.type()).toEqual('section');
	});

	it("Should contain as many children as there are work examples", () => {
		expect(component.find("ExampleWorkProject").length).toEqual(myWork.length);
	});
});

describe("ExampleWorkProject component", () => {
	let component = shallow(<ExampleWorkProject example={myWork[1]} />);

	let images = component.find("img");

	it("Should contain a single 'img' element", () => {
		expect(images.length).toEqual(1);
	});

	it("Should have the image src set correctly", () => {
		expect(images.node.props.src).toEqual(myWork[1].image.src);
	});
});
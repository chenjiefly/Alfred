'use strict';
const alfy = require('alfy');
const itemList = require('./data');

const items = alfy.inputMatches(
  itemList,
  'body'
).map(o => ({
  title: o.title,
  subtitle: o.body,
  arg: o.comment
}));

alfy.output(items);



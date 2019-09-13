var express = require('express');
var app = express();
var cors = require('cors');
var vsx = require('./vsx-830_telnet.js');

app.use(cors());

app.get('/', function (req, res) {
  res.json("Pedro's smarthome gateway - beta 0.1");
});

/**
 * VSX-830 receiver section.
 * All elements here control the VSX-830 through telnet.
 */

//Configure server name and other stuff.
vsx.params = {
   debug : false,
   command : '?V',
   expected : 'VOL',
   ip : '192.168.1.222'
 }

 //POWER STATUS
 app.get('/vsx/power/', function(req, res){
   vsx.params.expected = 'PWR'
   vsx.params.command = '?P';
   vsx.execute(vsx.params).then(function () {
     answer = (answer.match(/PWR1/))? 'off' : 'on';
     res.json({value:answer})
   }).catch(function (error){
     res.status(400).send('Error while requesting for power status!');
   });
 });

//POWER ON/OFF
app.post('/vsx/power/:val', function(req, res){
  let val = req.params.val;
  if( val !== 'on' && val !== 'off'){
    res.status(400).send('Valid options are "on" or "off", you sent "'+val+'".');
  }else{
    vsx.params.expected = 'PWR'
    vsx.params.command = (val === 'on')? 'PO' : 'PF';
    vsx.execute(vsx.params).then(function () {
      answer = (answer.match(/PWR1/))? 'on' : 'off'
      res.json({value:answer})
    }).catch(function (error){
      res.status(400).send('denied');
    });
  }
});

//VOLUME UP
app.post('/vsx/volume/up/', function (req, res) {
  vsx.params.expected = 'VOL'
  vsx.params.command = 'VU';
  vsx.execute(vsx.params).then(function () {
    res.json({value:answer})
  }).catch(function (error){
    res.status(400).send('denied');
  });
});

//VOLUME DOWN
app.post('/vsx/volume/down/', function (req, res) {
  vsx.params.expected = 'VOL'
  vsx.params.command = 'VD';
  vsx.execute(vsx.params).then(function () {
    answer = (answer.match(/PWR1/))? 'off' : 'on';
    res.json({value:answer})
  }).catch(function (error){
    res.status(400).send('denied');
  });
});

//GET VOLUME
app.get('/vsx/volume/', function(req, res){
  vsx.params.expected = 'VOL'
  vsx.params.command = '?V';
  vsx.execute(vsx.params).then(function () {
    //strip the VOL0 from the beggining
    answer = answer.replace(/VOL(0)?/g, '');
    //strip the \n from the end
    answer = answer.replace(/^[\s\n]+|[\s\n]+$/g, '');
    res.json({value:answer})
  }).catch(function (error){
    res.status(400).send('Cannot retrieve volume from receiver!');
  });
});

app.listen(8181, function () {
  console.log('Pedro smarthome gateway listening on port 8181!');
});


module.exports = {
  /**
   * Execute a command on VSX-830 receiver, should also work on telnet based
   * Pioneer receivers VSX-930, VSX-921, VSX-1021, and so on.
   *
   * I tried hard to reuse the telnet modules of nodejs however they all failed
   * to authenticate with the simple API. I then went debugging the telnet
   * protocol which is quite low level and takes a lot of time. So after a while
   * I decided to build this module that uses the telnet command.
   * Please verify that you have telnet command working before
   * using it. It is very simple to install telnet, brew install telnet (OSX),
   * apt-get install telnet (Linux), etc.
   *
   * Thanks to raymondjulin for the kickoff
   * https://raymondjulin.com/blog/remote-control-your-pioneer-vsx-receiver-over-telnet
   */
  execute : function(params){
    let debug    = (params.debug    !== undefined )? params.debug    : false;
    let ip       = (params.ip       !== undefined )? params.ip       : '192.168.1.222';
    let cmd      = (params.command  !== undefined )? params.command  : '?V';
    let expected = (params.expected !== undefined )? params.expected : 'VOL';
    let ms       = (params.timeout  !== undefined )? params.timeout  : 2000;
    let tries    = (params.tries    !== undefined )? params.tries    : 5;

    answer = undefined; //no answer yet

    return new Promise((resolve, reject) => {
      const dispatcher = require('child_process');
      const telnet = dispatcher.spawn('telnet', [ip]);

      timer = setTimeout(() => {
        telnet.kill();
        reject('Timed out in '+ ms + 'ms.');
      }, ms)

      finishSession = function() {
        if(debug){
            console.log('Finishing telnet connection.');
        }
        //send control command GS (group separator) or ^] (see ASCII)
        telnet.stdin.write(Buffer.from([0x1D]));
        //close telnet connection
        telnet.stdin.write('close\n');
        //clear timeout
        clearTimeout(timer);
        //finish the telnet input
        telnet.stdin.end();
      }

      sendCR = function() {
        telnet.stdin.write('\n');
      }

      telnet.stdout.on('data', (data) => {
        if(debug){
          console.log('stdout==>', data.toString());
        }

        /*
        * E04 is the error code from the receiver: command error
        * it happens from time to time that the E04 appears at first
        * attempt with no particular reason, just retry
        */
        if(data.toString().match('BridgeCo AG Telnet server') ||
          data.toString().match('E04')) {
          //write command
          sendCR();
          setTimeout(sendCR, 100);
          if(debug){
            console.log('Trying to send : '+cmd+'\n');
          }
          telnet.stdin.write(cmd);
          if(tries-- === 0){
            finishSession();
          }
        }else if(data.toString().match(expected)) {
          answer = data.toString();
          if(debug){
            console.log('Current answer : ', answer);
          }
          finishSession();
        }
      });

      telnet.stderr.on('data', (data) => {
        console.log(data.toString());
        reject();
      });

      telnet.on('exit', (code) => {
        if(debug){
          console.log('Child exited with code '+code);
        }
        resolve();
      });
    })
  },
  params : {
      debug : false,
      command : '?P',
      expected : 'PWR',
      ip : 'localhost',
      timeout : 2000
  }
}

/**
 * Just a simple test of function to execute VSX command.
 */
function test(){
  execute(params).then(function () {
    console.log('Promise answer ', answer);
  }).catch(function (error){
    console.log(error, '\nTry to increase timeout and set debug to true');
  });
}

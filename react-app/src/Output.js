import PropTypes from 'prop-types';
import CircularProgress from '@material-ui/core/CircularProgress';
import Box from '@material-ui/core/Box';

function CircularProgressWithLabel(props) {
    return (
      <Box position="relative" display="inline-flex">
        <CircularProgress variant="determinate" {...props} />
        <Box
          top={0}
          left={130}
          bottom={0}
          right={0}
          position="absolute"
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <label for='progress label' className='proglabel'>{props.value}%</label>
        </Box>
      </Box>
    );
}
CircularProgressWithLabel.propTypes = {
    value: PropTypes.number.isRequired,
};

const Output = () => {

    var running = false;
    var finished = true;
    var progress = 50
    var probeF = 'ATGC'
    var probeQ = 'ATGC'
    var sink = 'ATGC'
    var sinkC = 'ATGC'

    if(running) {
        return (
            <div className="progress">
                <h2>Optimization in Progress...</h2>
                <CircularProgressWithLabel variant="determinate" size='150px' value={progress} className="progressbar"/>
            </div>
        );
    }
    else if (finished) {
        return (
            <div className="outputsequences">
                <h2>Output</h2>
                <div className="sequencelabels">
                    <p>ProbeF: </p>
                    <p>ProbeQ: </p>
                    <p>Sink: </p>
                    <p>Sink*: </p>
                </div>
                <div className="outsequences">
                    <p>{probeF}</p>
                    <p>{probeQ}</p>
                    <p>{sink}</p>
                    <p>{sinkC}</p>
                </div>
            </div>
        );
    }
    else {
        return (
            <div className="emptyoutput">
                <h2>Output</h2>
            </div>
        );
    }

};

export default Output;
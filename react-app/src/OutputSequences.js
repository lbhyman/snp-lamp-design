const OutputSequences = () => {
    var probeF = '';
    var probeQ = '';
    var sink = '';
    var sinkC = '';

    return (
        <div className="outputsequences">
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
};

export default OutputSequences;
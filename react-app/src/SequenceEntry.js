const SequenceEntry = () => {
    return (
        <div className="sequenceentry">
            <div class="seq-form" id="non-mut-form">
                <label for="non-mut">WT Sequence</label>
                <input type="text" id="non-mut" name="non-mut" />
            </div>
            <div class="seq-form" id="mut-form">
                <label for="mut">Mutated Sequence</label>
                <input type="text" id="mut" name="mut" />
            </div>
        </div>
    );
};

export default SequenceEntry;
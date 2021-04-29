const Main = () => {
    // Slider
    const sliderMin = 16;
    const sliderMax = 4096;
    var sliderStart = 128;
    var sliderValue = sliderStart;
    const [value, setValue] = useState(Math.log2(sliderValue));
    const handleSlider = (event, newValue) => {
        setValue(newValue);
    };

    if(running) {

    }
    else if(finished) {
        
    }
    else {
        
    }
    return (
        <div className="PopSlider">
            <Typography variant="caption" className="sliderlabel" color='caption'>{`${2 ** value}`}</Typography>
            <Slider
                defaultValue={Math.log2(sliderValue)}
                getAriaValueText={valuetext}
                aria-labelledby="discrete-slider"
                valueLabelDisplay="auto"
                onChange={handleSlider}
                step={1}
                marks
                scale={(x) => 2 ** x}
                min={Math.log2(sliderMin)}
                max={Math.log2(sliderMax)}
            />
        </div>
    );
};

export default Main;
const ConditionEntry = () => {
    return (
        <div className="conditionentry">
            <div class="condition-form" id="temperature-form">
                <label for="temperature">Temperature (C)</label>
                <input type="text" id="temperature" name="temperature" />
            </div>
            <div class="condition-form" id="sodium-form">
                <label for="sodium">[Sodium] (mM)</label>
                <input type="text" id="sodium" name="sodium" />
            </div>
            <div class="condition-form" id="magnesium-form">
                <label for="magnesium">[Magnesium] (mM)</label>
                <input type="text" id="magnesium" name="magnesium" />
            </div>
        </div>
    );
};

export default ConditionEntry;
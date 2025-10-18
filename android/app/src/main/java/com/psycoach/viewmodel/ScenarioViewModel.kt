package com.psycoach.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.psycoach.data.model.ChoiceApplyResponse
import com.psycoach.data.model.Scenario
import com.psycoach.data.model.ScenarioDetail
import com.psycoach.data.repository.ScenarioRepository
import com.psycoach.domain.util.Result
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

@HiltViewModel
class ScenarioViewModel @Inject constructor(
    private val scenarioRepository: ScenarioRepository
) : ViewModel() {

    private val _scenarioListState = MutableStateFlow<Result<List<Scenario>>?>(null)
    val scenarioListState: StateFlow<Result<List<Scenario>>?> = _scenarioListState.asStateFlow()

    private val _scenarioDetailState = MutableStateFlow<Result<ScenarioDetail>?>(null)
    val scenarioDetailState: StateFlow<Result<ScenarioDetail>?> = _scenarioDetailState.asStateFlow()

    private val _choiceResultState = MutableStateFlow<Result<ChoiceApplyResponse>?>(null)
    val choiceResultState: StateFlow<Result<ChoiceApplyResponse>?> = _choiceResultState.asStateFlow()

    fun getScenarios(role: String? = null, kind: String? = null) {
        _scenarioListState.value = Result.Loading
        viewModelScope.launch {
            _scenarioListState.value = scenarioRepository.getScenarios(role, kind)
        }
    }

    fun getScenarioById(id: Int) {
        _scenarioDetailState.value = Result.Loading
        viewModelScope.launch {
            _scenarioDetailState.value = scenarioRepository.getScenarioById(id)
        }
    }

    fun chooseOption(scenarioId: Int, choiceId: Int) {
        _choiceResultState.value = Result.Loading
        viewModelScope.launch {
            _choiceResultState.value = scenarioRepository.chooseOption(scenarioId, choiceId)
        }
    }

    fun clearChoiceResult() {
        _choiceResultState.value = null
    }
}

package com.psycoach.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.psycoach.data.model.ProgressResponse
import com.psycoach.data.repository.ProgressRepository
import com.psycoach.domain.util.Result
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

@HiltViewModel
class ProgressViewModel @Inject constructor(
    private val progressRepository: ProgressRepository
) : ViewModel() {

    private val _progressState = MutableStateFlow<Result<ProgressResponse>?>(null)
    val progressState: StateFlow<Result<ProgressResponse>?> = _progressState.asStateFlow()

    fun getProgress() {
        _progressState.value = Result.Loading
        viewModelScope.launch {
            _progressState.value = progressRepository.getProgress()
        }
    }

    fun sendMiniGameResult(type: String, score: Int) {
        _progressState.value = Result.Loading
        viewModelScope.launch {
            _progressState.value = progressRepository.sendMiniGameResult(type, score)
        }
    }
}

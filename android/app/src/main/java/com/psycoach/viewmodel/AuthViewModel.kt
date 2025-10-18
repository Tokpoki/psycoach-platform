package com.psycoach.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.psycoach.data.model.AuthResponse
import com.psycoach.data.repository.AuthRepository
import com.psycoach.domain.util.Result
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

@HiltViewModel
class AuthViewModel @Inject constructor(
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _authState = MutableStateFlow<Result<AuthResponse>?>(null)
    val authState: StateFlow<Result<AuthResponse>?> = _authState.asStateFlow()

    private val _authToken = MutableStateFlow(authRepository.getToken())
    val authToken: StateFlow<String?> = _authToken.asStateFlow()

    fun register(email: String, password: String, role: String) {
        _authState.value = Result.Loading
        viewModelScope.launch {
            val result = authRepository.register(email, password, role)
            _authState.value = result
            if (result is Result.Success) {
                _authToken.value = result.data.accessToken
            }
        }
    }

    fun login(email: String, password: String) {
        _authState.value = Result.Loading
        viewModelScope.launch {
            val result = authRepository.login(email, password)
            _authState.value = result
            if (result is Result.Success) {
                _authToken.value = result.data.accessToken
            }
        }
    }

    fun logout() {
        authRepository.logout()
        _authToken.value = null
    }
}

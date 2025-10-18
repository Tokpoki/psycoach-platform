package com.psycoach.ui.screen.scenario

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.psycoach.data.model.Scenario
import com.psycoach.domain.util.Result

@Composable
fun ScenarioListScreen(
    scenarioState: Result<List<Scenario>>?,
    onRefresh: (String?, String?) -> Unit,
    onScenarioClick: (Int) -> Unit,
    onOpenProgress: () -> Unit
) {
    val roleFilter = remember { mutableStateOf("") }
    val kindFilter = remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(text = "Сценарии", style = MaterialTheme.typography.headlineMedium)
        Spacer(modifier = Modifier.height(12.dp))
        OutlinedTextField(
            value = roleFilter.value,
            onValueChange = { roleFilter.value = it },
            modifier = Modifier.fillMaxWidth(),
            label = { Text("Роль") }
        )
        Spacer(modifier = Modifier.height(8.dp))
        OutlinedTextField(
            value = kindFilter.value,
            onValueChange = { kindFilter.value = it },
            modifier = Modifier.fillMaxWidth(),
            label = { Text("Тип") }
        )
        Spacer(modifier = Modifier.height(8.dp))
        Button(
            onClick = { onRefresh(roleFilter.value.ifBlank { null }, kindFilter.value.ifBlank { null }) },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Обновить")
        }
        Spacer(modifier = Modifier.height(8.dp))
        Button(
            onClick = onOpenProgress,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Прогресс")
        }
        Spacer(modifier = Modifier.height(16.dp))
        when (scenarioState) {
            is Result.Loading -> {
                BoxedLoader()
            }
            is Result.Success -> {
                LazyColumn(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    items(scenarioState.data) { scenario ->
                        ScenarioItem(scenario = scenario, onClick = { onScenarioClick(scenario.id) })
                    }
                }
            }
            is Result.Error -> {
                Text(text = scenarioState.message, color = MaterialTheme.colorScheme.error)
            }
            null -> {
                Text(text = "Нажмите обновить для загрузки сценариев")
            }
        }
    }
}

@Composable
private fun ScenarioItem(scenario: Scenario, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(text = scenario.title, style = MaterialTheme.typography.titleMedium)
            Spacer(modifier = Modifier.height(4.dp))
            Text(text = "Роль: ${scenario.role}")
            Text(text = "Тип: ${scenario.kind}")
        }
    }
}

@Composable
private fun BoxedLoader() {
    Column(
        modifier = Modifier
            .fillMaxWidth(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        CircularProgressIndicator()
    }
}

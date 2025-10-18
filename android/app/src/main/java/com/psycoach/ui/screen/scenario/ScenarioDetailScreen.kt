package com.psycoach.ui.screen.scenario

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.psycoach.data.model.Choice
import com.psycoach.data.model.ChoiceApplyResponse
import com.psycoach.data.model.ScenarioDetail
import com.psycoach.domain.util.Result

@Composable
fun ScenarioDetailScreen(
    scenarioState: Result<ScenarioDetail>?,
    choiceState: Result<ChoiceApplyResponse>?,
    onChoiceSelected: (Int) -> Unit,
    onBack: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        when (scenarioState) {
            is Result.Loading -> Loader()
            is Result.Success -> {
                val scenario = scenarioState.data
                Text(text = scenario.title, style = MaterialTheme.typography.headlineSmall)
                Spacer(modifier = Modifier.height(12.dp))
                Text(text = scenario.description)
                Spacer(modifier = Modifier.height(16.dp))
                scenario.choices.forEach { choice ->
                    ChoiceCard(choice = choice, onChoiceSelected = onChoiceSelected)
                }
                Spacer(modifier = Modifier.height(16.dp))
                when (choiceState) {
                    is Result.Loading -> Loader()
                    is Result.Success -> ChoiceResult(choiceState.data)
                    is Result.Error -> Text(
                        text = choiceState.message,
                        color = MaterialTheme.colorScheme.error
                    )
                    null -> Unit
                }
            }
            is Result.Error -> {
                Text(text = scenarioState.message, color = MaterialTheme.colorScheme.error)
            }
            null -> {
                Text(text = "Загрузка...")
            }
        }
        Spacer(modifier = Modifier.weight(1f, fill = true))
        Button(onClick = onBack, modifier = Modifier.fillMaxWidth()) {
            Text(text = "Назад")
        }
    }
}

@Composable
private fun ChoiceCard(choice: Choice, onChoiceSelected: (Int) -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(text = choice.text, style = MaterialTheme.typography.bodyLarge)
            Spacer(modifier = Modifier.height(8.dp))
            Button(onClick = { onChoiceSelected(choice.id) }) {
                Text(text = "Выбрать")
            }
        }
    }
}

@Composable
private fun ChoiceResult(choiceResult: ChoiceApplyResponse) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(text = "Результат: ${choiceResult.result}", style = MaterialTheme.typography.titleMedium)
            Spacer(modifier = Modifier.height(8.dp))
            Text(text = choiceResult.explanation)
            Spacer(modifier = Modifier.height(4.dp))
            Text(text = "Изменение очков: ${choiceResult.score_delta}")
        }
    }
}

@Composable
private fun Loader() {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        CircularProgressIndicator()
    }
}

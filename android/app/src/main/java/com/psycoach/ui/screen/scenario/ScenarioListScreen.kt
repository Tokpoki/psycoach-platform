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
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
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

private val RoleOptions = listOf(
    "Any role" to null,
    "Athlete" to "athlete",
    "Coach" to "coach",
    "Parent" to "parent",
    "Psychologist" to "psychologist",
    "Admin" to "admin"
)

private val KindOptions = listOf(
    "All types" to null,
    "Prestart" to "prestart",
    "Defeat" to "defeat",
    "Conflict" to "conflict",
    "Judgement" to "judgement",
    "Injury" to "injury"
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ScenarioListScreen(
    scenarioState: Result<List<Scenario>>?,
    onRefresh: (String?, String?) -> Unit,
    onScenarioClick: (Int) -> Unit,
    onOpenProgress: () -> Unit
) {
    val roleExpanded = remember { mutableStateOf(false) }
    val kindExpanded = remember { mutableStateOf(false) }
    val selectedRole = remember { mutableStateOf(RoleOptions.first()) }
    val selectedKind = remember { mutableStateOf(KindOptions.first()) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(text = "Scenarios", style = MaterialTheme.typography.headlineMedium)
        Spacer(modifier = Modifier.height(12.dp))

        ExposedDropdownMenuBox(
            expanded = roleExpanded.value,
            onExpandedChange = { roleExpanded.value = !roleExpanded.value }
        ) {
            OutlinedTextField(
                value = selectedRole.value.first,
                onValueChange = {},
                modifier = Modifier
                    .menuAnchor()
                    .fillMaxWidth(),
                label = { Text("Role") },
                readOnly = true,
                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = roleExpanded.value) },
                colors = ExposedDropdownMenuDefaults.textFieldColors()
            )
            DropdownMenu(
                expanded = roleExpanded.value,
                onDismissRequest = { roleExpanded.value = false }
            ) {
                RoleOptions.forEach { option ->
                    DropdownMenuItem(
                        text = { Text(option.first) },
                        onClick = {
                            selectedRole.value = option
                            roleExpanded.value = false
                        }
                    )
                }
            }
        }

        Spacer(modifier = Modifier.height(8.dp))

        ExposedDropdownMenuBox(
            expanded = kindExpanded.value,
            onExpandedChange = { kindExpanded.value = !kindExpanded.value }
        ) {
            OutlinedTextField(
                value = selectedKind.value.first,
                onValueChange = {},
                modifier = Modifier
                    .menuAnchor()
                    .fillMaxWidth(),
                label = { Text("Type") },
                readOnly = true,
                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = kindExpanded.value) },
                colors = ExposedDropdownMenuDefaults.textFieldColors()
            )
            DropdownMenu(
                expanded = kindExpanded.value,
                onDismissRequest = { kindExpanded.value = false }
            ) {
                KindOptions.forEach { option ->
                    DropdownMenuItem(
                        text = { Text(option.first) },
                        onClick = {
                            selectedKind.value = option
                            kindExpanded.value = false
                        }
                    )
                }
            }
        }

        Spacer(modifier = Modifier.height(8.dp))

        Button(
            onClick = { onRefresh(selectedRole.value.second, selectedKind.value.second) },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Refresh")
        }

        Spacer(modifier = Modifier.height(8.dp))

        Button(
            onClick = onOpenProgress,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Progress")
        }

        Spacer(modifier = Modifier.height(16.dp))

        when (scenarioState) {
            is Result.Loading -> BoxedLoader()
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
                Text(text = "Select filters and tap Refresh to load scenarios.")
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
            Text(
                text = "Role: ${scenario.role ?: "Any"}",
                style = MaterialTheme.typography.bodyMedium
            )
            Text(
                text = "Type: ${scenario.kind ?: "—"}",
                style = MaterialTheme.typography.bodyMedium
            )
        }
    }
}

@Composable
private fun BoxedLoader() {
    Column(
        modifier = Modifier.fillMaxWidth(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        CircularProgressIndicator()
    }
}

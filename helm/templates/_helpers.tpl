{{- define "verify-slackConfig" -}}
{{- if not (or (.Values.slack.apiToken) (.Values.slack)) }}
{{- fail "Slack configuration cannot be empty. Define the Slack API key and Default Email" }}
{{- end }}
{{- end -}}


{{/*
Expand the name of the chart.
*/}}
{{- define "failedkite.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "failedkite.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if hasPrefix .Release.Name $name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "failedkite.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "failedkite.labels" -}}
helm.sh/chart: {{ include "failedkite.chart" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "failedkite.selectorLabels" -}}
app.kubernetes.io/name: {{ include "failedkite.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app: {{ include "failedkite.name" . }}
{{- end }}
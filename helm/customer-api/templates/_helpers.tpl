{{/*
Generate the full name of the application
*/}}
{{- define "customer-api.fullname" -}}
{{- printf "%s-%s" .Release.Name "customer-api" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

# Configure Notification Templates

## Template Syntax (Go Template) Description

The alert notification template uses [Go Template](https://pkg.go.dev/text/template) syntax to render the template.

The template will be rendered based on the following data.

```json
{
    "status": "firing",
    "labels": {
        "alertgroup": "test-group",           // Alert policy name
        "alertname": "test-rule",          // Alert rule name
        "cluster": "35b54a48-b66c-467b-a8dc-503c40826330",
        "customlabel1": "v1",
        "customlabel2": "v2",
        "endpoint": "https",
        "group_id": "01gypg06fcdf7rmqc4ksv97646",
        "instance": "10.6.152.85:6443",
        "job": "apiserver",
        "namespace": "default",
        "prometheus": "insight-system/insight-agent-kube-prometh-prometheus",
        "prometheus_replica": "prometheus-insight-agent-kube-prometh-prometheus-0",
        "rule_id": "01gypg06fcyn2g9zyehbrvcdfn",
        "service": "kubernetes",
        "severity": "critical",
        "target": "35b54a48-b66c-467b-a8dc-503c40826330",
        "target_type": "cluster"
   },
    "annotations": {
        "customanno1": "v1",
        "customanno2": "v2",
        "description": "This is a test rule, 10.6.152.85:6443 down",
        "value": "1"
    },
    "startsAt": "2023-04-20T07:53:54.637363473Z",
    "endsAt": "0001-01-01T00:00:00Z",
    "generatorURL": "http://vmalert-insight-victoria-metrics-k8s-stack-df987997b-npsl9:8080/vmalert/alert?group_id=16797738747470868115&alert_id=10071735367745833597",
    "fingerprint": "25c8d93d5bf58ac4"
}
```

### Instructions for Use

1. `.` character

    Render the specified object in the current scope.

    Example 1: Take all content under the top-level scope, which is all of the context data in the example code.

    ```go
    {{ . }}
    ```

2. Conditional statement __if / else__

    Use __if__ to check the data and run __else__ if it does not meet.

    ```go
    {{if .Labels.namespace }}Namespace: {{ .Labels.namespace }} \n{{ end }}
    ```

3. Loop feature __for__ 

    The __for__ feature is used to repeat the code content.

    Example 1: Traverse the labels list to obtain all label content for alerts.

    ```go
    {{ for .Labels}} \n {{end}}
    ```

## FUNCTIONS

Insight's "notification templates" and "SMS templates" support over 70 [sprig](http://masterminds.github.io/sprig/) functions, as well as custom functions.

### Sprig Functions

Sprig provides over 70 built-in template functions to assist in rendering data. The following are some commonly used functions:

* [Date operations](http://masterminds.github.io/sprig/date.html)
* [String operations](http://masterminds.github.io/sprig/strings.html)
* [Type conversion operations](http://masterminds.github.io/sprig/conversion.html)
* [Mathematical calculations with integers](http://masterminds.github.io/sprig/math.html)

For more details, you can refer to the [official documentation](http://masterminds.github.io/sprig/).

### Custom Functions

#### toClusterName

The __toClusterName__ function retrieves the "cluster name" based on the "cluster unique identifier (ID)". If there is no corresponding cluster found, it will directly return the passed-in cluster's unique identifier.

```go
func toClusterName(id string) (string, error)
```

**Example:**

```go-templates
{{ toClusterName "clusterId" }}
{{ "clusterId" | toClusterName }}
```

#### toClusterId

The __toClusterId__ function retrieves the "cluster unique identifier (ID)" based on the "cluster name". If there is no corresponding cluster found, it will directly return the passed-in cluster name.

```go
func toClusterId(name string) (string, error)
```

**Example:**

```go-templates
{{ toClusterId "clusterName" }}
{{ "clusterName" | toClusterId }}
```

#### toDateInZone

The __toDateInZone__ function converts a string date into the desired time format and applies the specified time zone.

```go
func toDateInZone(fmt string, date interface{}, zone string) string
```

**Example 1**:

```go-templates
{{ toDateInZone "2006-01-02T15:04:05" "2022-08-15T05:59:08.064449533Z" "Asia/Shanghai" }}
```

This will return __2022-08-15T13:59:08__. Additionally, you can achieve the same effect as __toDateInZone__ using the built-in functions provided by sprig:

```go-templates
{{ dateInZone "2006-01-02T15:04:05" (toDate "2006-01-02T15:04:05Z07:00" .StartsAt) "Asia/Shanghai" }}
```

**Example 2**:

```go-templates
{{ toDateInZone "2006-01-02T15:04:05" .StartsAt "Asia/Shanghai" }}

## Threshold Template Description

The built-in webhook alert template in Insight is as follows. Other contents such as email and WeCom are the same, only corresponding adjustments are made for line breaks.

```text
Rule Name: {{ .Labels.alertname }} \n
Policy Name: {{ .Labels.alertgroup }} \n
Alert level: {{ .Labels.severity }} \n
Cluster: {{ .Labels.cluster }} \n
{{if .Labels.namespace }}Namespace: {{ .Labels.namespace }} \n{{ end }}
{{if .Labels.node }}Node: {{ .Labels.node }} \n{{ end }}
Resource Type: {{ .Labels.target_type }} \n
{{if .Labels.target }}Resource Name: {{ .Labels.target }} \n{{ end }}
Trigger Value: {{ .Annotations.value }} \n
Occurred Time: {{ .StartsAt }} \n
{{if ne "0001-01-01T00:00:00Z" .EndsAt }}End Time: {{ .EndsAt }} \n{{ end }}
Description: {{ .Annotations.description }} \n
```

### Email Subject Parameters

Because Insight combines messages generated by the same rule at the same time when sending alert messages, email subjects are different from the four templates above and only use the content of commonLabels in the alert message to render the template. The default template is as follows:

```go
[{{ .status }}] [{{ .severity }}] Alert: {{ .alertname }}
```

Other fields that can be used as email subjects are as follows:

```text
{{ .status }} Triggering status of the alert message
{{ .alertgroup }} Name of the policy to which the alert belongs
{{ .alertname }} Name of the rule to which the alert belongs
{{ .severity }} Severity level of the alert
{{ .target_type }} Type of resource for which the alert is raised
{{ .target }} Resource object for which the alert is raised
{{ .Custom label key for other rules }}
```

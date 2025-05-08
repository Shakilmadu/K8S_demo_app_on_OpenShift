# k8s_demo.py
# Python-based demonstration of Kubernetes features using the Kubernetes Python client

from kubernetes import client, config

# Load Kubernetes config (assumes access to kubeconfig or running in-cluster)
config.load_kube_config()  # or config.load_incluster_config()

v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()
batch_v1 = client.BatchV1Api()
batch_v1beta1 = client.BatchV1beta1Api()
autoscaling_v1 = client.AutoscalingV1Api()
rbac_v1 = client.RbacAuthorizationV1Api()
networking_v1 = client.NetworkingV1Api()

# Namespace creation
def create_namespace():
    ns = client.V1Namespace(metadata=client.V1ObjectMeta(name="demo-namespace"))
    v1.create_namespace(ns)

# Pod definition
def create_pod():
    pod_manifest = client.V1Pod(
        metadata=client.V1ObjectMeta(name="demo-pod"),
        spec=client.V1PodSpec(containers=[
            client.V1Container(
                name="nginx",
                image="nginx",
                ports=[client.V1ContainerPort(container_port=80)]
            )
        ])
    )
    v1.create_namespaced_pod(namespace="demo-namespace", body=pod_manifest)

# Deployment
def create_deployment():
    container = client.V1Container(
        name="nginx",
        image="nginx",
        ports=[client.V1ContainerPort(container_port=80)]
    )
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "nginx"}),
        spec=client.V1PodSpec(containers=[container])
    )
    spec = client.V1DeploymentSpec(
        replicas=3,
        selector={'matchLabels': {'app': 'nginx'}},
        template=template
    )
    deployment = client.V1Deployment(
        metadata=client.V1ObjectMeta(name="nginx-deployment"),
        spec=spec
    )
    apps_v1.create_namespaced_deployment(namespace="demo-namespace", body=deployment)

# Service (ClusterIP)
def create_service():
    service = client.V1Service(
        metadata=client.V1ObjectMeta(name="nginx-service"),
        spec=client.V1ServiceSpec(
            selector={"app": "nginx"},
            ports=[client.V1ServicePort(port=80, target_port=80)],
            type="ClusterIP"
        )
    )
    v1.create_namespaced_service(namespace="demo-namespace", body=service)

# ConfigMap
def create_configmap():
    config_map = client.V1ConfigMap(
        metadata=client.V1ObjectMeta(name="demo-config"),
        data={"example.key": "value"}
    )
    v1.create_namespaced_config_map(namespace="demo-namespace", body=config_map)

# Secret
def create_secret():
    secret = client.V1Secret(
        metadata=client.V1ObjectMeta(name="demo-secret"),
        string_data={"password": "supersecret"},
        type="Opaque"
    )
    v1.create_namespaced_secret(namespace="demo-namespace", body=secret)

# Job
def create_job():
    container = client.V1Container(name="pi", image="perl", command=["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"])
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"job": "pi"}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container])
    )
    job_spec = client.V1JobSpec(template=template, backoff_limit=4)
    job = client.V1Job(metadata=client.V1ObjectMeta(name="pi-job"), spec=job_spec)
    batch_v1.create_namespaced_job(namespace="demo-namespace", body=job)

# Main entry
if __name__ == "__main__":
    create_namespace()
    create_pod()
    create_deployment()
    create_service()
    create_configmap()
    create_secret()
    create_job()
    print("K8s demo resources created in 'demo-namespace'.")


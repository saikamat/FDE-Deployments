FROM public.ecr.aws/lambda/python:3.11

# Install build dependencies for compiling Python packages
RUN yum update -y && \
    yum install -y gcc gcc-c++ make && \
    yum clean all

# Optional: set working dir in Lambda task root
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source and artifacts into the image
COPY app/ ./app/
COPY artifacts/ ./artifacts/

# CMD is the Lambda handler string: module.submodule:variable_or_callable
CMD ["app.main.handler"]
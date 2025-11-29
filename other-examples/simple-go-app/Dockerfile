# --- Stage 1: The Builder ---
# We use a large image with the Go compiler installed
FROM golang:1.23 AS builder

WORKDIR /app

# Initialize a module and copy source code
# (In a real app, you'd copy go.mod/go.sum first to cache dependencies)
COPY main.go .
RUN go mod init myapp

# Compile the binary
# CGO_ENABLED=0 ensures a static binary with no external C dependencies
RUN CGO_ENABLED=0 GOOS=linux go build -o my-binary main.go

# --- Stage 2: The Runner ---
# We use a tiny image (Alpine Linux) for the final product
FROM alpine:latest

WORKDIR /root/

# Copy ONLY the compiled binary from the "builder" stage
COPY --from=builder /app/my-binary .

# Expose the port
EXPOSE 8080

# Run the binary
CMD ["./my-binary"]
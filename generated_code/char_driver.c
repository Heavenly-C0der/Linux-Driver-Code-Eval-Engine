#include <linux/module.h>
#include <linux/fs.h>
#include <linux/uaccess.h>

#define DEVICE_NAME "char_buffer"
#define BUF_LEN 1024

static int major;
static char msg[BUF_LEN];
static int open(struct inode *, struct file *);
static int release(struct inode *, struct file *);
static ssize_t read(struct file *, char *, size_t, loff_t *);
static ssize_t write(struct file *, const char *, size_t, loff_t *);

static struct file_operations fops = {
    .read = read,
    .write = write,
    .open = open,
    .release = release
};

static int open(struct inode *inode, struct file *file) {
    return 0;
}

static int release(struct inode *inode, struct file *file) {
    return 0;
}

static ssize_t read(struct file *filp, char *buffer, size_t len, loff_t *offset) {
    copy_to_user(buffer, msg, len);
    return len;
}

static ssize_t write(struct file *filp, const char *buffer, size_t len, loff_t *offset) {
    copy_from_user(msg, buffer, len);
    return len;
}

static int __init char_init(void) {
    major = register_chrdev(0, DEVICE_NAME, &fops);
    return 0;
}

static void __exit char_exit(void) {
    unregister_chrdev(major, DEVICE_NAME);
}

module_init(char_init);
module_exit(char_exit);
MODULE_LICENSE("GPL");

mod app;
mod domain;

use app::health::healthcheck;

fn main() {
    println!("ERP Desktop Core :: {}", healthcheck());
}
